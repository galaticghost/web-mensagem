import { useEffect, useState } from "react"
import { searchUsers } from "../../service/userService";
import { createPrivateChat, getUserChats } from "../../service/chatService";
import "../../styles/chatSidebar.css";
import type { User, Chat } from "../../types/types";

interface ChatSidebarProps {
    onSelectChat: (id: number) => void;
}

export default function ChatSidebar({ onSelectChat }: ChatSidebarProps) {
    const [username, setUsername] = useState<string>("");
    const [searchedUsers, setSearchedUsers] = useState<User[] | null>(null);
    const [chats, setChats] = useState<Chat[] | null>(null);

    const loadChats = async () => {
        const data = await getUserChats();
        setChats(data.chats);
    }

    useEffect(() => {
        loadChats();
    }, []);

    const handleChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
        setUsername(e.target.value);// TODO Debounce
        if (e.target.value.length > 2) {
            try {
                setSearchedUsers(await searchUsers(e.target.value));
            } catch (error: unknown) {
                if (error instanceof Error) {
                    console.error(error.message);
                }
            }
        }
    }

    const handleAddUser = async (id: number) => {
        await createPrivateChat(id);
        setUsername("");
        setSearchedUsers(null);
        await loadChats();
    }

    return (
        <section className="chat-sidebar">
            <section>
                <label htmlFor="add">Adicione alguem</label>
                <input type="text" name="add" value={username}
                    onChange={handleChange} />
                {searchedUsers &&
                    <ul>
                        {searchedUsers.map((user) => (
                            <li key={user.id}>
                                <p>{user.username}</p>
                                <button onClick={() => handleAddUser(user.id)}>Add</button>
                            </li>
                        ))}
                    </ul>
                }
            </section>
            <section>
                {chats &&
                    <ul>
                        {chats.map((chat) => (
                            <li key={chat.id}>
                                <button onClick={() => onSelectChat(chat.id)}>
                                    <p>{chat.display_name}</p>
                                </button>
                            </li>
                        ))}
                    </ul>
                }
            </section>
        </section>
    )
}