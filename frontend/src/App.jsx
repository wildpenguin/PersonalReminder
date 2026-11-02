import { useEffect, useState } from "react";

const EMPTY_FORM = { title: "", message: "", due: "", priority: "normal", repeat: false };

export default function App() {
  const [reminders, setReminders] = useState([]);
  const [form, setForm] = useState(EMPTY_FORM);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch("/reminders")
      .then((response) => {
        if (!response.ok) throw new Error(`Could not load reminders (${response.status})`);
        return response.json();
      })
      .then(setReminders)
      .catch((err) => setError(err.message));
  }, []);

  function handleChange(event) {
    const { name, value, type, checked } = event.target;
    setForm({ ...form, [name]: type === "checkbox" ? checked : value });
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setError(null);
    try {
      const response = await fetch("/reminders", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        // The <input type="datetime-local"> value has no timezone, which the API rejects.
        // new Date() reads it as local time and toISOString() sends it as UTC.
        body: JSON.stringify({ ...form, due: new Date(form.due).toISOString() }),
      });
      if (!response.ok) throw new Error(`Could not save reminder (${response.status})`);
      const created = await response.json();
      setReminders([...reminders, created]);
      setForm(EMPTY_FORM);
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <main>
      <h1>Reminders</h1>

      {error && <p className="error">{error}</p>}

      <form onSubmit={handleSubmit}>
        <label>
          Title
          <input name="title" value={form.title} onChange={handleChange} required />
        </label>
        <label>
          Message
          <input name="message" value={form.message} onChange={handleChange} />
        </label>
        <label>
          Due
          <input name="due" type="datetime-local" value={form.due} onChange={handleChange} required />
        </label>
        <label>
          Priority
          <select name="priority" value={form.priority} onChange={handleChange}>
            <option value="low">Low</option>
            <option value="normal">Normal</option>
            <option value="high">High</option>
          </select>
        </label>
        <label className="checkbox">
          <input name="repeat" type="checkbox" checked={form.repeat} onChange={handleChange} />
          Repeat
        </label>
        <button type="submit">Add reminder</button>
      </form>

      {reminders.length === 0 ? (
        <p>No reminders yet.</p>
      ) : (
        <ul>
          {reminders.map((reminder) => (
            <li key={reminder.id}>
              <strong>{reminder.title}</strong>
              {reminder.message && <span> — {reminder.message}</span>}
              <div className="meta">
                {new Date(reminder.due).toLocaleString()} · {reminder.priority}
                {reminder.repeat && " · repeats"}
              </div>
            </li>
          ))}
        </ul>
      )}
    </main>
  );
}
