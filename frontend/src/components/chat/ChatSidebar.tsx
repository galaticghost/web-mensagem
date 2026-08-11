import { useEffect, useState } from "react"
import { getUserChats } from "../../service/chatService";
import "../../styles/chatSidebar.css";
import type { Chat } from "../../types/types";
import ChatHeader from "./ChatHeader";
import { websocket } from "../../websockets/socket";

interface ChatSidebarProps {
    setChat: (chat: Chat) => void;
    chatId: number | undefined;
}

export default function ChatSidebar({ setChat, chatId }: ChatSidebarProps) {
    const [chats, setChats] = useState<Chat[]>([]);
    const [search, setSearch] = useState<string>("");
    const [searchedChats, setSearchedChats] = useState<Chat[]>([]);
//    const [notifications, setNotifications] = useState<Notification[]>([]);
    
    const loadChats = async () => {
        const data = await getUserChats();
        setChats(data.chats);
    }

    useEffect(() => {
        if (chats && search) {
            const filterChats = chats.filter((chat) =>
                chat.display_name.toLowerCase().includes(search.toLowerCase())
            )
            setSearchedChats([...filterChats]);
        }

        if (search.length < 1) {
            setSearchedChats([]);
        }
    }, [search])

    useEffect(() => {
        loadChats();
    }, []);

    useEffect(() => {
        websocket.onNotification((message) => {
            if (chatId && message.chat_id !== chatId) {
                const notification = {
                    
                }
                //setNotifications((prev) => [...prev, notification]);
            }
        })
    },[])

    return (
        <aside className="chat-sidebar">
            <ChatHeader
                search={search}
                setSearch={setSearch}
                chats={chats}
                loadChats={loadChats}
            />
            <section>

                {searchedChats.length > 0 && chats ?           
                    <ul>
                        {searchedChats.map((chat) => (
                            <li key={chat.id}>
                                <button onClick={() => setChat(chat)}>
                                    <p>{chat.display_name}</p>
                                </button>
                            </li>
                        ))}
                    </ul>
                    :
                    <ul>
                        {chats.map((chat) => (
                            <li key={chat.id}>
                                <button onClick={() => setChat(chat)}>
                                    <p>{chat.display_name}</p>
                                </button>
                            </li>
                        ))}
                    </ul>}
            </section>
        </aside>
    )
}