import { useCallback, useEffect, useState } from "react"
import type { User } from "../../types/types";
import { debounce } from "../../utils/utils";
import { searchUsers } from "../../service/userService";
import UserItem from "./UserItem";
import { createGroupChat } from "../../service/chatService";

interface CreateGroupProps {
    loadChats: () => Promise<void>;
    onClose: () => void;
    setIsCreatePrivate: () => void;
}

export default function CreateGroup({ loadChats, onClose, setIsCreatePrivate }: CreateGroupProps) {
    const [isSelectingUsers, setIsSelectingUsers] = useState<boolean>(false)
    const [name, setName] = useState<string>("");
    const [description, setDescription] = useState<string>("");
    const [searchedUsers, setSearchedUsers] = useState<User[]>([]);
    const [selectedUsers, setSelectedUsers] = useState<number[]>([]);
    const [username, setUsername] = useState<string>("");

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

    const handleToggleUser = (id: number) => {
        setSelectedUsers(prev =>
            prev.includes(id)
                ? prev.filter(userId => userId !== id)
                : [...prev, id]
        );
    };

    const goToUserSelection = () => {
        if (name.trim().length < 3) {
            return;
        }

        setIsSelectingUsers(true);
    };

    const handleGroupCreation = async () => {
        if (name.trim().length < 3) {
            return;
        }

        if (selectedUsers.length === 0) {
            return;
        }
        await createGroupChat(selectedUsers, name, description);

        setUsername("");
        setDescription("");
        setName("");
        setSelectedUsers([]);
        setSearchedUsers([]);

        await loadChats();
        onClose();
    }

    const changeToPrivate = () => {
        setUsername("");
        setDescription("");
        setName("");
        setSelectedUsers([]);
        setSearchedUsers([]);
        setIsCreatePrivate();
    }

    return (
        <section className="group-info">
            {isSelectingUsers ?
                <>
                    <div className="group-navigation">
                        <button onClick={() => setIsSelectingUsers(false)}>{'<-'}</button>
                        <p>Adicionar participantes</p>
                        <input type="text" name="add" value={username}
                            onChange={(e) => setUsername(e.target.value.trim())} />
                    </div>
                    {searchedUsers.length > 0 &&
                        <ul>
                            {searchedUsers.map((user) => {
                                const added = selectedUsers.includes(user.id);

                                return (
                                    <UserItem
                                        key={user.id}
                                        user={user}
                                        handleAddUser={handleToggleUser}
                                        added={added}
                                        disabled={false}
                                        buttonText={added ? "Remover" : "Adicionar"}
                                    />
                                )
                            })}
                        </ul>
                    }
                    <button onClick={handleGroupCreation}>Criar</button>
                </>
                :
                <>
                    <div className="group-navigation">
                        <button onClick={changeToPrivate}>{'←'}</button>
                        <p>Criar grupo</p>
                    </div>
                    <label htmlFor="groupName" >Nome do grupo</label>
                    <input
                        id="groupName"
                        name="groupName"
                        type="text"
                        required={true}
                        minLength={3}
                        maxLength={50}
                        onChange={(e) => setName(e.target.value.trim())}
                        value={name}
                        placeholder="Digite o nome do grupo..."
                    />
                    <label htmlFor="groupDescription">Descrição</label>
                    <input
                        id="groupDescription"
                        name="groupDescription"
                        type="text"
                        value={description}
                        maxLength={500}
                        onChange={(e) => setDescription(e.target.value.trim())}
                        placeholder="Descrição do grupo..."
                    />
                    <button onClick={goToUserSelection}>{'Próximo →'}</button>
                </>
            }
        </section>
    )
}