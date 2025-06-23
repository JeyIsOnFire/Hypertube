//We need a FormData for special inputs (File..) which mean a basic JSON stringify can't work.
export function convertToFormData(formData: {[key: string]: string | File | null}): FormData {
    const formDataConvert = new FormData();

    for (const key in formData) {
      const value = formData[key];

      if (value === null || value === undefined) continue;

      if (value instanceof File)
        formDataConvert.append(key, value);
      else
        formDataConvert.append(key, String(value));
    }
    return formDataConvert;
}

export function isDataFilled(data: string[]): boolean {
    return data.every((value) => value.trim() !== '')
}