import { useEffect } from "react";

interface SearchChatBar {
    search: string,
    setSearch: (value: string) => void;
}

export default function SearchChatBar({search, setSearch}: SearchChatBar) {

    return (
        <>
            <input 
                type="text"
                id="chat"
                name="chat"
                maxLength={50}
                value={search}
                onChange={(e) => setSearch(e.target.value)}
            />
        </>
    )
}