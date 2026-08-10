import { useEffect, useState } from "react"
import { getUserChats } from "../../service/chatService";
import "../../styles/chatSidebar.css";
import type { Chat } from "../../types/types";
import ChatHeader from "./ChatHeader";

interface ChatSidebarProps {
    onSelectChat: (chat: Chat) => void;
}

export default function ChatSidebar({ onSelectChat }: ChatSidebarProps) {
    const [chats, setChats] = useState<Chat[]>([]);
    const [search, setSearch] = useState<string>("");

    const loadChats = async () => {
        const data = await getUserChats();
        setChats(data.chats);
    }

    useEffect(() => {
        if (chats && search) {
            const filterChats = chats.filter((chat) =>
                chat.display_name.toLowerCase().includes(search.toLowerCase())
            )
            console.log(filterChats)
        }
    }, [search])

    useEffect(() => {
        loadChats();
    }, []);

    return (
        <aside className="chat-sidebar">
            <ChatHeader
                search={search}
                setSearch={setSearch}
                chats={chats}
                loadChats={loadChats}
            />
            <section>
                {chats &&
                    <ul>
                        {chats.map((chat) => (
                            <li key={chat.id}>
                                <button onClick={() => onSelectChat(chat)}>
                                    <p>{chat.display_name}</p>
                                </button>
                            </li>
                        ))}
                    </ul>
                }
            </section>
        </aside>
    )
}