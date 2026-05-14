import { render, screen } from "@testing-library/react";
import App from "./App";

test("renders RAG chatbot UI", () => {
  render(<App />);

  const titleElement = screen.getByText(/rag chatbot/i);
  expect(titleElement).toBeInTheDocument();
});

test("renders website input", () => {
  render(<App />);

  const inputElement = screen.getByPlaceholderText(/enter website url/i);
  expect(inputElement).toBeInTheDocument();
});

test("renders PDF upload input", () => {
  render(<App />);

  const fileInput = screen.getByLabelText(/upload pdf/i);
  expect(fileInput).toBeInTheDocument();
});

test("renders chat input", () => {
  render(<App />);

  const chatInput = screen.getByPlaceholderText(/ask a question/i);
  expect(chatInput).toBeInTheDocument();
});

test("renders send button", () => {
  render(<App />);

  const sendButton = screen.getByText(/send/i);
  expect(sendButton).toBeInTheDocument();
});