import { useState } from "react";

const API = "http://localhost:5555";

function AuthForm({ onLogin }) {
    const [mode, setMode] = useState("login");
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    async function handleSubmit(e) {
        e.preventDefault();
        setError("");
        try{
            const res = await fetch(`${API}/${mode}`, {
                method: "POST",
                credentials: "include",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, password }),
            });
            const data = await res.json();
            if (res.ok) {
                onLogin(data);
            } else{
              setError(data.error);  
            }
        } catch {
          setError("Could not reach the server");  
        }
    }

    return (
        <form onSubmit={handleSubmit}>
            <h2>{mode === "login" ? "Log in" : "Sign up"}</h2>
            <input
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Username"
            />
            <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Password"
            />
            <button type="submit">{mode === "login" ? "Log in" : "Create account"}</button>
            {error && <p style={{ color: "red" }}>{error}</p>}
            <button type="button" onClick={() => setMode(mode === "login" ? "signup" : "login")}>
                {mode === "login" ? "New account?" : "Have an account?"}
            </button>
        </form>
    );
}

export default AuthForm;