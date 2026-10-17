import { useState, useEffect } from 'react';
import AuthForm from './AuthForm';

const API = "http://localhost:5555";

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);	

  useEffect(() => {
    fetch(`${API}/check_session`, { credentials: "include" })
      .then((res) => (res.ok ? res.json() : null))
      .then((data) => {
        setUser(data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  },  []);

  function handleLogout() {
    fetch(`${API}/logout`, { method: "DELETE", credentials: "include" })
      .then(() => setUser(null));
  }

if (loading) return <p>Checking...</p>;
if (!user) return <AuthForm onLogin={setUser} />;
  return (
    <div>
      <h1>Welcome, {user.username}!</h1>
      <button onClick={handleLogout}>Log out</button>
    </div>
  );
}

export default App;
