import SearchChatBar from "./SearchChatBar";
import { useAuth } from "../../hooks/useAuth";
import { useState } from "react";
import Modal from "../Modal";
import AddChat from "./AddChat";
import type { Chat } from "../../types/types";
import CreateGroup from "./CreateGroup";

interface ChatHeaderProps {
    search: string;
    setSearch: (value: string) => void;
    loadChats: () => Promise<void>;
    chats: Chat[];
}

export default function ChatHeader({ search, setSearch, loadChats, chats }: ChatHeaderProps) {
    const { logout } = useAuth();
    const [isModalOpen, setIsModalOpen] = useState<boolean>(false);
    const [isCreatePrivate, setIsCreatePrivate] = useState<boolean>(true);

    const handleCloseModal = () => {
        setIsModalOpen(false);
        setIsCreatePrivate(true);
    };

    const handleOpenModal = () => {
        setIsCreatePrivate(true);
        setIsModalOpen(true);
    };

    return (
        <section>
            <section>
                <h2>Web-Mensagens</h2>
                <button onClick={handleOpenModal}>AddChat</button>
                <button onClick={logout}>Logout</button>
                {isModalOpen &&
                    <Modal onClose={() => handleCloseModal()}>
                        {isCreatePrivate ?
                            <AddChat loadChats={loadChats}
                                onClose={() => handleCloseModal()} chats={chats}
                                setIsCreatePrivate={() => setIsCreatePrivate(false)} />
                            :
                            <CreateGroup
                                loadChats={loadChats}
                                onClose={() => handleCloseModal()}
                                setIsCreatePrivate={() => setIsCreatePrivate(true)} />
                        }
                    </Modal>
                }
            </section>
            <SearchChatBar
                search={search}
                setSearch={setSearch}
            />
        </section>
    )
}