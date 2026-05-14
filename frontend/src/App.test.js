import { render, screen } from "@testing-library/react";
import App from "./App";

test("renders RAG chatbot UI", () => {
  render(<App />);

  const titleElement = screen.getByText(/rag chatbot/i);
  expect(titleElement).toBeInTheDocument();
});