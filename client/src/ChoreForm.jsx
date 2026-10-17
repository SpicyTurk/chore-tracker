import { useState } from "react";

const API = "http://localhost:5555"

function ChoreForm({ onCreated }) {
    const [title, setTitle] = useState("");
    const [due, setDue] = useState("");
    const [assignee, setAssignee] = useState("");
    const [error, setError] = useState("");

    async function handleSubmit(e) {
        e.preventDefault();
        setError("");
        try {
            const res = await fetch(`${API}/chores`, {
                method: "POST",
                credentials: "include",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ title, due, assignee }),
            });
            const data = await res.json();
            if (res.ok) {
                setTitle("");
                setDue("");
                setAssignee("");
                onCreated();
            } else{
                setError(data.error);
            }
        } catch {
            setError("Could not reach the server");
        }
    }


    return (
        <form onSubmit={handleSubmit}>
            <h3>New chore</h3>
            <input value={title} onChange={(e) => setTitle(e.target.value)} placeholder="Title" />
            <input type="date" value={due} onChange={(e) => setDue(e.target.value)} />
            <input value={assignee} onChange={(e) => setAssignee(e.target.value)} placeholder="Assignees username" />
            <button type="submit">Add new chore</button>
            {error && <p style={{ color: "red" }}>{error}</p>}
        </form>
    );
}

export default ChoreForm;