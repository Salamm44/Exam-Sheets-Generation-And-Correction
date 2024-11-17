import { toast } from 'react-toastify';

function TestToast() {
  const notify = () => {
    toast('This is a test!', {
      position: "top-center",
      autoClose: 5000,
      hideProgressBar: false,
      closeOnClick: true,
      pauseOnHover: true,
      draggable: true,
      progress: undefined,
    });
  }

  return (
    <button onClick={notify}>Test Toast</button>
  );
}

export default TestToast;