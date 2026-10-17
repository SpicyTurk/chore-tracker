import { useState, useEffect } from 'react';

const API = "http://localhost:5555";
const PER_PAGE = 5;

function formatDate(text) {
    const [year, month, day] = text.split("-").map(Number);
    return new Date(year, month - 1, day).toLocaleDateString("en-US", {
        month: "short",
        day: "numeric",
        year: "numeric",
    });
}

function ChoreList({ reloadKey }) {
  const [chores, setChores] = useState([]);
  const [page, setPage] = useState(1);
  const [pages, setPages] = useState(1);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadChores() {
        try {
            const res = await fetch(
                `${API}/chores?page=${page}&per_page=${PER_PAGE}`,
                { credentials: "include" }
            );
            const data = await res.json();
            if (res.ok) {
                setChores(data.chores);
                setPages(data.pages);
                setError("");
            } else {
                setError(data.error);
            }
        } catch {
            setError("Could not reach the server");
        }
    }
    loadChores();
  }, [page, reloadKey]);

  return (
    <div>
      <h2>Chores</h2>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <ul style={{ listStyle: "none", padding: 0 }}>
        {chores.map((c) => (
          <li key={c.id} style={{ marginBottom: "1rem" }}>
            <strong>{c.title}</strong>
            {c.status === "overdue" && <span style={{ color: "red" }}> Overdue</span>}
            {c.status === "completed" && <span style={{ color: "green" }}> Completed</span>}
            <div>
                {c.completed_on
                    ? `Completed: ${new Date(c.completed_on).toLocaleString("en-US", { dateStyle: "medium", timeStyle: "short" })} By: ${c.assignee}`
                    : `Due Date: ${formatDate(c.due_date)}`}
                    </div>
            <div>Created by {c.creator} - Assigned to {c.assignee}</div>
          </li>
        ))}
        </ul>
        <button onClick={() => setPage(page - 1)} disabled={page <= 1}>Previous</button>
        <span> Page {page} of {Math.max(pages, 1)} </span>
        <button onClick={() => setPage(page + 1)} disabled={page >= pages}>Next</button>
        </div>
    );
}

export default ChoreList;