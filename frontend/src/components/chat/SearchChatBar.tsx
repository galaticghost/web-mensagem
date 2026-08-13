import searchIcon from "../../assets/icons/search.svg";

interface SearchChatBar {
    search: string;
    setSearch: (value: string) => void;
}

export default function SearchChatBar({ search, setSearch }: SearchChatBar) {
    return (
        <div className="search-bar">
            <img src={searchIcon} alt="Ícone de procura" className="icon" />
            <input
                className="searchbar"
                type="text"
                id="chat"
                name="chat"
                maxLength={50}
                value={search}
                placeholder="Procure um chat"
                onChange={(e) => setSearch(e.target.value)}
            />
        </div>
    )
}