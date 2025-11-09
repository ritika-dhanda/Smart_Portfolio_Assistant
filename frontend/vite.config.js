import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      "/chatbot": "http://127.0.0.1:8000",
      "/resume": "http://127.0.0.1:8000",
    },
  },
});
