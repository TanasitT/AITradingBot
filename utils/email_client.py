import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECIPIENT


def send_email(subject, body_text, body_html=None):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECIPIENT

    msg.attach(MIMEText(body_text, "plain"))
    if body_html:
        msg.attach(MIMEText(body_html, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECIPIENT, msg.as_string())


def send_trade_alert(action, symbol, shares, price, stop_loss, thesis, score):
    subject = f"Trade Bot — {action} {symbol} @ ${price:.2f}"
    text = (
        f"{action} {shares} shares of {symbol} at ${price:.2f}\n"
        f"Stop-loss set at ${stop_loss:.2f}\n"
        f"Research score: {score}/100\n\n"
        f"Thesis: {thesis}"
    )
    send_email(subject, text)


def send_halt_alert(reason, portfolio_value, daily_pnl_pct):
    subject = f"Trade Bot — HALTED | Daily loss {daily_pnl_pct:.2%}"
    text = (
        f"Trading halted for today.\n\n"
        f"Reason: {reason}\n"
        f"Portfolio value: ${portfolio_value:,.2f}\n"
        f"Daily P&L: {daily_pnl_pct:.2%}\n\n"
        f"All routines suspended until tomorrow market open."
    )
    send_email(subject, text)


def send_stop_loss_alert(symbol, entry, exit_price, shares, pnl):
    subject = f"Trade Bot — Stop-loss hit {symbol} | P&L: ${pnl:+.2f}"
    text = (
        f"Stop-loss triggered for {symbol}\n"
        f"Entry: ${entry:.2f} | Exit: ${exit_price:.2f} | Shares: {shares}\n"
        f"P&L: ${pnl:+.2f}"
    )
    send_email(subject, text)
