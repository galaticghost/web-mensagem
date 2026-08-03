import "../../styles/chatWindow.css";

interface ChatWindowProps {
    chatId: number | null;
}

export default function ChatWindow({ chatId }: ChatWindowProps) {

    if (!chatId) {
        return (
            <section className="chat-window">
                <p>Teste</p>
            </section>
        )
    }

    return (
        <section className="chat-window">
            Chat selecionado: {chatId}
        </section>
    )
}