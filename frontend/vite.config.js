import { defineConfig } from "vite";

export default defineConfig({
  server: {
    // During `npm run dev`, send API requests to the FastAPI server.
    proxy: {
      "/reminders": "http://127.0.0.1:8000",
    },
  },
});
