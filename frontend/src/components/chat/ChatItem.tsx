import type { Chat } from "../../types/types";

interface ChatItemProps {
    chat: Chat;
    setChat: (chat: Chat) => void;
}

export default function ChatItem ({chat, setChat}: ChatItemProps) {
    return (
        <li key={chat.id}>
            <button onClick={() => setChat(chat)}>
                <p>{chat.display_name}</p>
            </button>
        </li>
    )
}