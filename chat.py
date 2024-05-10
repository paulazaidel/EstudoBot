import logging
import os

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

from const import CHAT_TOKEN
from geminia import GeminiIa

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="💡 Olá! Sabia que responder perguntas sobre o que você estudou é uma ótima maneira de memorizar melhor o conteúdo? 🧠 Ao buscar as respostas, você reforça as conexões neurais e consolida o aprendizado.",
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="📚 Quer testar seus conhecimentos e turbinar sua memorização? Me envie um arquivo PDF com o conteúdo que você está estudando e eu gero 10 perguntas e respostas para você! 😉",
    )


async def handle_document_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Recebe o arquivo PDF do usuário."""

    # Obtém o documento
    document = update.message.document

    # Cria a pasta 'files' se ela não existir
    if not os.path.exists("files"):
        os.makedirs("files")

    # Obtém o nome do arquivo
    filename = document.file_name

    # Obtém o arquivo do Telegram
    file = await document.get_file()

    # Baixa o arquivo e salva na pasta 'files'
    await file.download_to_drive(f"files/{filename}")

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"✅ Gerando suas perguntas...",
    )

    # Gera as perguntas usando IA
    response = GeminiIa().execute(filename)

    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=response, parse_mode="Markdown"
    )


async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="❌ Desculpe, só posso processar arquivos PDF.",
    )


if __name__ == "__main__":
    application = ApplicationBuilder().token(CHAT_TOKEN).build()

    start_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, start)
    document_pdf_handler = MessageHandler(filters.Document.PDF, handle_document_pdf)
    document_handler = MessageHandler(~filters.Document.PDF, handle_document)

    application.add_handler(start_handler)
    application.add_handler(document_pdf_handler)
    application.add_handler(document_handler)

    application.run_polling()
