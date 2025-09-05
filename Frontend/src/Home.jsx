import React, { useState } from 'react';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import Below from './components/Below';
import About from './components/About';
import Footer from './components/Footer';


const Home = () => {
    return(
     <>
      
      <Navbar />
      <Hero />
      <About />
      <Below />
      <Footer />
      
     </>
    )
};

export default Home;
