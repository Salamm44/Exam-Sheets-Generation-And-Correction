export const isFormEmpty = (form) => {
    return Object.values(form).every(value => value === '');
  };