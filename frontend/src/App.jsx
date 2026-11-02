import { useEffect, useState } from "react";

const EMPTY_FORM = { title: "", message: "", due: "", priority: "normal", repeat: false };

export default function App() {
  const [reminders, setReminders] = useState([]);
  const [form, setForm] = useState(EMPTY_FORM);
  const [error, setError] = useState(null);
  const [saving, setSaving] = useState(false);

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
    setSaving(true);
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
    } finally {
      setSaving(false);
    }
  }

  const sorted = [...reminders].sort((a, b) => new Date(a.due) - new Date(b.due));

  return (
    <main>
      <header className="page-header">
        <h1>Reminders</h1>
        <p>Schedule desktop notifications for your Mac.</p>
      </header>

      {error && (
        <p className="error" role="alert">
          {error}
        </p>
      )}

      <div className="layout">
        <section className="card" aria-labelledby="add-heading">
          <h2 id="add-heading">New reminder</h2>

          <form onSubmit={handleSubmit}>
            <label className="field">
              <span>Title</span>
              <input
                name="title"
                value={form.title}
                onChange={handleChange}
                placeholder="e.g. Stand-up meeting"
                required
              />
            </label>

            <label className="field">
              <span>Message</span>
              <textarea
                name="message"
                value={form.message}
                onChange={handleChange}
                placeholder="Optional details"
                rows={3}
              />
            </label>

            <div className="row">
              <label className="field">
                <span>Due</span>
                <input
                  name="due"
                  type="datetime-local"
                  value={form.due}
                  onChange={handleChange}
                  required
                />
              </label>

              <label className="field">
                <span>Priority</span>
                <select name="priority" value={form.priority} onChange={handleChange}>
                  <option value="low">Low</option>
                  <option value="normal">Normal</option>
                  <option value="high">High</option>
                </select>
              </label>
            </div>

            <label className="checkbox">
              <input name="repeat" type="checkbox" checked={form.repeat} onChange={handleChange} />
              <span>Repeat every day at this time</span>
            </label>

            <button type="submit" className="primary" disabled={saving}>
              {saving ? "Saving…" : "Add reminder"}
            </button>
          </form>
        </section>

        <section className="card" aria-labelledby="list-heading">
          <h2 id="list-heading">
            Your reminders <span className="count">{reminders.length}</span>
          </h2>

          {sorted.length === 0 ? (
            <p className="empty">No reminders yet. Add one to get started.</p>
          ) : (
            <ul className="reminders">
              {sorted.map((reminder) => (
                <li key={reminder.id} className={`reminder priority-${reminder.priority}`}>
                  <div className="reminder-title">{reminder.title}</div>
                  {reminder.message && <div className="reminder-message">{reminder.message}</div>}
                  <div className="reminder-meta">
                    <time dateTime={reminder.due}>
                      {new Date(reminder.due).toLocaleString(undefined, {
                        dateStyle: "medium",
                        timeStyle: "short",
                      })}
                    </time>
                    <span className={`badge badge-${reminder.priority}`}>{reminder.priority}</span>
                    {reminder.repeat && <span className="badge">Daily</span>}
                  </div>
                </li>
              ))}
            </ul>
          )}
        </section>
      </div>
    </main>
  );
}
