import { getOrigin } from '$lib/GenerateUrl/store';

export function dataToRequestParam(
  username: string,
  password: string,
  teamId: string | null = null
): string {
  const data: Record<string, string> = {
    username,
    password
  };
  if (teamId) data['team_id'] = teamId;

  const jsonData = JSON.stringify(data);
  const base64Data = window.btoa(jsonData);
  return encodeURIComponent(base64Data);
}

export async function generateRequestPayload(
  username: string,
  password: string,
  teamId: string | null = null
): Promise<string> {
  const origin = getOrigin();
  const data: Record<string, string> = {
    username,
    password
  };
  if (teamId) data['team_id'] = teamId;

  const request = await fetch(`${origin}/api/generate_request_payload`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
    credentials: 'omit'
  });
  const text = await request.text();
  return encodeURIComponent(text);
}
