import type { JSX } from "react"
import "../styles/modal.css"

interface ModalProps {
    children: JSX.Element;
    onClose: () => void;
}

export default function Modal({ children, onClose }: ModalProps) {
    return (
        <div className="modal" >
            <div className="modal-overlay" onClick={onClose} />
            <section className="modal-box">
                {children}
            </section>
        </div>
    )
}