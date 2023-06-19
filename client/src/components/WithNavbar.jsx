import React from 'react';
import Navbar from './Navbar';


const withNavbar = (WrappedComponent) => {
  return (props) => (
    <div>
      <Navbar/>
      <WrappedComponent {...props} />
    </div>
  );
};

export default withNavbar;
