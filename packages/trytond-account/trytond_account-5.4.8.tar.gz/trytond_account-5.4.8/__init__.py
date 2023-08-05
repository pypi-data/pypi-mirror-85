# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.pool import Pool
from .fiscalyear import *
from .account import *
from . import configuration
from .period import *
from .journal import *
from .move import *
from .move_template import *
from . import tax
from . import party


def register():
    Pool.register(
        FiscalYear,
        BalanceNonDeferralStart,
        TypeTemplate,
        Type,
        AccountTemplate,
        AccountTemplateTaxTemplate,
        Account,
        AccountDeferral,
        AccountTax,
        OpenChartAccountStart,
        GeneralLedgerAccount,
        GeneralLedgerAccountContext,
        GeneralLedgerLine,
        GeneralLedgerLineContext,
        BalanceSheetContext,
        BalanceSheetComparisionContext,
        IncomeStatementContext,
        CreateChartStart,
        CreateChartAccount,
        CreateChartProperties,
        UpdateChartStart,
        UpdateChartSucceed,
        AgedBalanceContext,
        AgedBalance,
        configuration.Configuration,
        configuration.ConfigurationDefaultAccount,
        configuration.DefaultTaxRule,
        Period,
        Journal,
        JournalSequence,
        JournalCashContext,
        JournalPeriod,
        Move,
        Reconciliation,
        configuration.ConfigurationTaxRounding,
        Line,
        WriteOff,
        OpenJournalAsk,
        ReconcileLinesWriteOff,
        ReconcileShow,
        CancelMovesDefault,
        GroupLinesStart,
        PrintGeneralJournalStart,
        tax.TaxGroup,
        tax.TaxCodeTemplate,
        tax.TaxCode,
        tax.TaxCodeLineTemplate,
        tax.TaxCodeLine,
        tax.OpenChartTaxCodeStart,
        tax.TaxTemplate,
        tax.Tax,
        tax.TaxLine,
        tax.TaxRuleTemplate,
        tax.TaxRule,
        tax.TaxRuleLineTemplate,
        tax.TaxRuleLine,
        tax.TestTaxView,
        tax.TestTaxViewResult,
        MoveTemplate,
        MoveTemplateKeyword,
        MoveLineTemplate,
        TaxLineTemplate,
        CreateMoveTemplate,
        CreateMoveKeywords,
        party.Party,
        party.PartyAccount,
        RenewFiscalYearStart,
        module='account', type_='model')
    Pool.register(
        OpenType,
        BalanceNonDeferral,
        OpenChartAccount,
        CreateChart,
        UpdateChart,
        OpenJournal,
        OpenAccount,
        ReconcileLines,
        UnreconcileLines,
        Reconcile,
        CancelMoves,
        GroupLines,
        PrintGeneralJournal,
        CreateMove,
        tax.OpenChartTaxCode,
        tax.OpenTaxCode,
        tax.TestTax,
        party.PartyReplace,
        party.PartyErase,
        RenewFiscalYear,
        module='account', type_='wizard')
    Pool.register(
        GeneralLedger,
        TrialBalance,
        AgedBalanceReport,
        GeneralJournal,
        module='account', type_='report')
