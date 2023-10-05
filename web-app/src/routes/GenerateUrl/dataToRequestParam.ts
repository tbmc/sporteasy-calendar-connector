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
