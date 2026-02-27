import axios from "axios";
import { BACKEND_URL } from "./config";

export async function invokeAgent(payload: {
  user_id: string;
  session_id: string;
  query: string;
}) {
  const res = await axios.post(`${BACKEND_URL}/invoke`, payload, {
    headers: {
      "Content-Type": "application/json",
    },
  });

  return res.data;
}
