export const fetchApi = async (endpoint: string) => {
  try {
    const url = process.env.NEXT_PUBLIC_HOSTNAME;
    console.log("url", url);
    const response = await fetch(`https://${process.env.NEXT_PUBLIC_HOSTNAME}:8443/api/${endpoint}`, {
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    const data = await response.json();
    return data;
  } catch (error) {
    throw error;
  }
}; 