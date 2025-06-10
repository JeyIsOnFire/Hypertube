export const fetchApi = async (endpoint: string) => {

  try {
    const url = process.env.NEXT_PUBLIC_HOSTNAME;
    console.log("url", url);
    const response = await fetch(`${process.env.NEXT_PUBLIC_HOSTNAME}:8443/movies/` + endpoint);
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    const data = await response.json();
    return data;
  } catch (error) {
    throw error;
  }
};

/*
** If the function got a 403 error (unauthorized) the logout function will be called (not implemented yet).
** Credentials MUST BE provided (user must be logged in).
*/
export async function postData(url: string, data: any) {
    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: data instanceof FormData ? undefined : {
          "Content-Type": "application/json",
        },
        body: data,
        credentials: "include"
      });

      if (!response.ok) {
        const errorData = await response.json();
        console.log(`Error when POST on URL ${url}: ${errorData}`);
        return false;
      }

      const result = await response.json();
      console.log(`Successfully POST on URL ${url}: ${result}`);
      return true;
    } catch (err) {
      console.log(`Error when POST on URL ${url}: ${err}`);
      return false;
    }
}

