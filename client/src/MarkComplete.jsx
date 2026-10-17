import { useState } from "react";

const API = "http://localhost:5555";

function MarkComplete({ choreId, onCompleted }) {
    const [when, setWhen] = useState("");
    const [error, setError] = useState("");

    async function handleSubmit(e) {
        e.preventDefault();
        setError("");
        try {
            const res = await fetch(`${API}/chores/${choreId}/completion`, {
                method: "POST",
                credentials: "include",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ completed_on: when }),
            });
            if (res.ok) {
                setWhen("");
                onCompleted();
            } else {
                const data = await res.json();
                setError(data.error);
            } 
        }    catch {
                setError("Could not reach the server");
            }
        }

    return (
        <form onSubmit={handleSubmit}>
            <input type="datetime-local" value={when} onChange={(e) => setWhen(e.target.value)} />
            <button type="submit">Mark as completed</button>
            {error && <span style={{ color: "red" }}>{error}</span>}
        </form>
    );
}

export default MarkComplete;