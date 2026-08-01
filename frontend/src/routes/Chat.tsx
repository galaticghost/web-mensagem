import { useState } from "react"
import { searchUsers } from "../service/userService";
import { createPrivateChat } from "../service/chatService";
import type { User } from "../types/types";

export default function Chat() {
    const [username, setUsername] = useState<string>("");
    const [searchedUsers, setSearchedUsers] = useState<User[] | null>(null);

    const handleChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
        setUsername(e.target.value);
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
    }

    return (
        <main>
            <section>
                Chats
            </section>
            <section>
                <label htmlFor="add">Adicione alguem</label>
                <input type="text" name="add" value={username}
                    onChange={handleChange} />
                {searchedUsers &&
                    <ul>
                        {searchedUsers.map((user, index) => (
                            <li key={index}>
                                <p>{user.username}</p>
                                <button onClick={() => handleAddUser(user.id)}>Add</button>
                            </li>
                        ))}
                    </ul>
                }

            </section>
        </main>
    )
}