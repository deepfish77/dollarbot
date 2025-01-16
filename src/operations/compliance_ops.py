import logging
from src.queries.compliance_queries import log_compliance_issue, resolve_compliance_issue

logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.INFO)

class ComplianceService:
    """
    A service to handle compliance issues from Stripe webhooks.
    """

    @staticmethod
    def handle_account_update(account):
        """
        Handle the account.updated webhook event.
        """
        account_id = account["id"]
        requirements = account.get("requirements", {})
        disabled_reason = requirements.get("disabled_reason")

        if disabled_reason:
            issue_type = "account_disabled"
            description = f"Account disabled due to: {disabled_reason}"
            log_compliance_issue(account_id, issue_type, description)
            logger.warning("Compliance issue logged: %s", description)
            return {"status": "issue_logged", "reason": disabled_reason}
        else:
            resolve_compliance_issue(account_id, "account_disabled")
            logger.info("Account compliance issue resolved for account_id: %s", account_id)
            return {"status": "resolved"}

    @staticmethod
    def handle_transfer_failed(transfer):
        """
        Handle the transfer.failed webhook event.
        """
        account_id = transfer["destination"]
        transfer_id = transfer["id"]
        failure_reason = transfer.get("failure_message", "Unknown reason")

        issue_type = "transfer_failed"
        description = f"Transfer {transfer_id} failed: {failure_reason}"
        log_compliance_issue(account_id, issue_type, description)
        logger.warning("Transfer failure logged: %s", description)
        return {"status": "issue_logged", "reason": failure_reason}
