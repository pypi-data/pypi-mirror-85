# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from trytond.pool import PoolMeta, Pool
from trytond.model import fields
from trytond.pyson import Eval, If, Bool
from trytond.transaction import Transaction

__all__ = ['Statement', 'StatementLine']


class Statement(metaclass=PoolMeta):
    __name__ = 'account.statement'

    @classmethod
    def create_move(cls, statements):
        pool = Pool()
        MoveLine = pool.get('account.move.line')
        Payment = pool.get('account.payment')

        moves = super(Statement, cls).create_move(statements)

        to_success = set()
        to_fail = set()
        for move, statement, lines in moves:
            for line in lines:
                if line.payment:
                    payments = {line.payment}
                    kind = line.payment.kind
                elif line.payment_group:
                    payments = set(line.payment_group.payments)
                    kind = line.payment_group.kind
                else:
                    continue
                if (kind == 'receivable') == (line.amount >= 0):
                    to_success.update(payments)
                else:
                    to_fail.update(payments)
        # The failing should be done last because success is usually not a
        # definitive state
        if to_success:
            Payment.succeed(Payment.browse(to_success))
        if to_fail:
            Payment.fail(Payment.browse(to_fail))

        for move, statement, lines in moves:
            assert len({l.payment for l in lines}) == 1
            line = lines[0]
            if line.payment and line.payment.clearing_move:
                clearing_account = line.payment.journal.clearing_account
                if clearing_account.reconcile:
                    to_reconcile = []
                    for line in move.lines + line.payment.clearing_move.lines:
                        if (line.account == clearing_account
                                and not line.reconciliation):
                            to_reconcile.append(line)
                    if not sum((l.debit - l.credit) for l in to_reconcile):
                        MoveLine.reconcile(to_reconcile)
        return moves

    def _group_key(self, line):
        key = super(Statement, self)._group_key(line)
        if hasattr(line, 'payment'):
            key += (('payment', line.payment),)
        return key


class StatementLine(metaclass=PoolMeta):
    __name__ = 'account.statement.line'
    payment = fields.Many2One('account.payment', 'Payment',
        domain=[
            If(Bool(Eval('party')), [('party', '=', Eval('party'))], []),
            ('state', 'in', ['processing', 'succeeded', 'failed']),
            ],
        states={
            'invisible': Bool(Eval('payment_group')) | Bool(Eval('invoice')),
            'readonly': Eval('statement_state') != 'draft',
            },
        depends=['party', 'statement_state'])
    payment_group = fields.Many2One(
        'account.payment.group', "Payment Group",
        domain=[
            ('company', '=', Eval('company', -1)),
            ],
        states={
            'invisible': Bool(Eval('payment')) | Bool(Eval('invoice')),
            'readonly': Eval('statement_state') != 'draft',
            },
        depends=['company', 'statement_state'])

    @classmethod
    def __setup__(cls):
        super(StatementLine, cls).__setup__()
        invoice_invisible = Bool(Eval('payment')) | Bool(Eval('payment_group'))
        if 'invisible' in cls.invoice.states:
            cls.invoice.states['invisible'] |= invoice_invisible
        else:
            cls.invoice.states['invisible'] = invoice_invisible

    @classmethod
    def copy(cls, lines, default=None):
        if default is None:
            default = {}
        else:
            default = default.copy()
        default.setdefault('payment', None)
        default.setdefault('payment_group', None)
        return super(StatementLine, cls).copy(lines, default=default)

    @fields.depends('payment', 'party', 'account', '_parent_statement.journal')
    def on_change_payment(self):
        pool = Pool()
        Currency = pool.get('currency.currency')
        if self.payment:
            if not self.party:
                self.party = self.payment.party
            clearing_account = self.payment.journal.clearing_account
            if not self.account and clearing_account:
                self.account = clearing_account
            if self.statement and self.statement.journal:
                with Transaction().set_context(date=self.payment.date):
                    amount = Currency.compute(self.payment.currency,
                        self.payment.amount, self.statement.journal.currency)
                self.amount = amount
                if self.payment.kind == 'payable':
                    self.amount *= -1

    @fields.depends('payment_group', 'account')
    def on_change_payment_group(self):
        if self.payment_group:
            self.party = None
            clearing_account = self.payment_group.journal.clearing_account
            if not self.account and clearing_account:
                self.account = clearing_account

    @fields.depends('party', 'payment')
    def on_change_party(self):
        super(StatementLine, self).on_change_party()
        if self.payment:
            if self.payment.party != self.party:
                self.payment = None
        self.payment_group = None

    @fields.depends('account', 'payment', 'payment_group')
    def on_change_account(self):
        super(StatementLine, self).on_change_account()
        if self.payment:
            clearing_account = self.payment.journal.clearing_account
        elif self.payment_group:
            clearing_account = self.payment_group.journal.clearing_account
        else:
            return
        if self.account != clearing_account:
            self.payment = None

    @classmethod
    def post_move(cls, lines):
        pool = Pool()
        Move = pool.get('account.move')
        super(StatementLine, cls).post_move(lines)
        Move.post([l.payment.clearing_move for l in lines
                if l.payment
                and l.payment.clearing_move
                and l.payment.clearing_move.state == 'draft'])
