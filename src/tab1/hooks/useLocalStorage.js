import { useState, useEffect, useRef } from 'react';

function useLocalStorage(key, initialValue= {}) {
  const readValue = () => {
    if (typeof window === 'undefined') {
      return initialValue;
    }

    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      return initialValue;
    }
  };

  const [storedValue, setStoredValue] = useState(readValue);
  const keyRef = useRef(key);

  const setValue = (value) => {
    if (typeof window == 'undefined') {
      console.warn(
        `Tried setting localStorage key “${key}” even though environment is not a client`
      );
    }

    try {
      const newValue = value instanceof Function ? value(storedValue) : value;
      if (newValue !== storedValue) {
        window.localStorage.setItem(key, JSON.stringify(newValue));
        setStoredValue(newValue);
      }
    } catch (error) {
      console.warn(`Error setting localStorage key “${key}”:`, error);
    }
  };

  useEffect(() => {
    if (key !== keyRef.current) {
      keyRef.current = key;
      setStoredValue(readValue());
    }
  }, [key]);

  return [storedValue, setValue];
}

export default useLocalStorage;