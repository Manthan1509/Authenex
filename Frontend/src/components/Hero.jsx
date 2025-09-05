import React from 'react';
import Lottie from 'lottie-react';
import CertificateAni from '../assets/Certificate Ani.json'; // your Lottie JSON file

const Hero = () => {
  return (
    <div className="flex items-center justify-center pt-10 pb-16 text-white bg-[#0A3258] relative overflow-hidden font-[Inter]">
      {/* TODO: Add background image here */}
      <div className="absolute top-0 left-0 w-full h-full bg-cover bg-center opacity-20 z-0"></div>
      
      <div className="container flex flex-col lg:flex-row items-center justify-between z-10 max-w-7xl mx-auto">
        <div className="text-center lg:text-left lg:w-2/3 mt-10 lg:mt-0">
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold leading-tight mb-4">
            Authenticate Academic Records in Seconds—with Security
          </h1>
          <p className="text-lg sm:text-[24px] leading-relaxed mt-9 mb-8">
            Authenex lets you instantly verify certificates with full security and reliability. Prevent fraud, save time, and trust every academic record you check.
          </p>
          <button className="bg-[#1C69D3] hover:bg-[#1554a9] text-white font-semibold mt-1 py-3 px-8 rounded-full shadow-lg transition duration-300 transform hover:scale-105 text-[20px]">
            Get Started
          </button>
        </div>
        
        <div className="lg:w-1/3 flex justify-center items-center mt-10 lg:mt-0">
          {/* Lottie Animation instead of Image */}
          <Lottie 
            animationData={CertificateAni} 
            loop={true} 
            className="h-[530px] w-[380px]" 
          />
        </div>
      </div>
    </div>
  );
};

export default Hero;
