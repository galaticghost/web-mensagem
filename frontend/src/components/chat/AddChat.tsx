import type { Chat, User } from "../../types/types";
import { useCallback, useEffect, useState } from "react";
import { debounce } from "../../utils/utils";
import { searchUsers } from "../../service/userService";
import { createPrivateChat } from "../../service/chatService";
import UserItem from "./UserItem";

interface AddChatProps {
    loadChats: () => Promise<void>;
    onClose: () => void;
    chats: Chat[];
    setIsCreatePrivate: () => void;
}

export default function AddChat({ loadChats, onClose, chats, setIsCreatePrivate }: AddChatProps) {
    const [username, setUsername] = useState<string>("");
    const [searchedUsers, setSearchedUsers] = useState<User[]>([]);

    useEffect(() => {
        if (username.length < 3) {
            setSearchedUsers([]);
            return;
        }
        handleSearch(username);
    }, [username])

    const handleSearch = useCallback(
        debounce(async (value: string) => {
            try {
                if (value.length < 3) {
                    return;
                }
                const users = await searchUsers(value);
                setSearchedUsers(users);
            } catch (error: unknown) {
                if (error instanceof Error) {
                    console.error(error.message);
                }
            }
        }),
        []
    );

    const hasPrivateChat = (userId: number) => {
        return chats.some(chat =>
            chat.type === "private" &&
            chat.users_id.includes(userId)
        );
    };

    const handleAddUser = async (id: number) => {
        try {
            await createPrivateChat(id);

            setUsername("");
            setSearchedUsers([]);

            await loadChats();
            onClose();
        } catch (error: unknown) {
            if (error instanceof Error) {
                console.error(error.message);
            }
        }
    }

    const changeToGroup = () => {
        setUsername("");
        setIsCreatePrivate();
    }

    return (

        <section>
            <button onClick={changeToGroup}> CRIAR GRUPO</button>
            <input type="text" name="add" value={username}
                className="search-bar-input"
                onChange={(e) => setUsername(e.target.value.trim())}
                placeholder="Digite um nome de usuário..." />

            {searchedUsers.length > 0 &&
                <ul>
                    {searchedUsers.map((user) => {
                        const added = hasPrivateChat(user.id);

                        return (
                            <UserItem
                                key={user.id}
                                user={user}
                                added={added}
                                disabled={added}
                                buttonText={added ? "Já existe" : "Adicionar"}
                                handleAddUser={handleAddUser}
                            />
                        );
                    })}
                </ul>
            }
        </section>
    )
}