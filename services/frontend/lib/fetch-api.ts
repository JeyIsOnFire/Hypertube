export const fetchApi = async (endpoint: string) => {

  try {
    const url = process.env.NEXT_PUBLIC_HOSTNAME;
    console.log("fetchApi call:", url);
    const response = await fetch(`http://localhost:7000/` + endpoint);
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    const data = await response.json();
    return data;
  } catch (error) {
    throw error;
  }
};

