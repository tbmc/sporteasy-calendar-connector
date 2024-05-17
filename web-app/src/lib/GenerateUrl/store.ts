import { writable } from 'svelte/store';
import { dataToRequestParam } from './dataToRequestParam';
import { browser, dev } from '$app/environment';

export const dataParamsStore = writable('');
export const disableSaveLoginStore = writable(false);

export const fetchTeamsIsLoading = writable(false);
export const fetchTeamsData = writable([]);
export const fetchTeamsLoadedOnce = writable(false);

export function getOrigin() {
  let origin = '';

  if (dev) {
    origin = 'http://localhost:5000';
  } else {
    origin = browser ? window.location.origin : '';
  }
  
  return `${origin}/api`;
}

export async function fetchTeamsGet(username: string, password: string) {
  fetchTeamsIsLoading.set(true);
  fetchTeamsData.set([]);

  const data = dataToRequestParam(username, password);

  try {
    const origin = getOrigin();
    const response = await fetch(`${origin}/list-teams?data=${data}`);
    fetchTeamsData.set(await response.json());
  } catch (e) {
    console.error(e);
  }
  fetchTeamsIsLoading.set(false);
  fetchTeamsLoadedOnce.set(true);
}
