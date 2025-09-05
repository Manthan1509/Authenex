import React from 'react';
import AboutLogo from '../assets/About_image_2.png';
import CheckLogo from '../assets/check.png';
import InstituteLogo from '../assets/bank.png';
import AlertLogo from '../assets/alert.png';
import ShieldLogo from '../assets/shield.png';

const About = () => {
  const features = [
    {
      title: "Instant Verification",
      description: "Verify certificates within seconds using our intuitive platform.",
      icon: CheckLogo,
    },
    {
      title: "Institute Dashboard",
      description: "Upload student records in bulk and verify certificates instantly.",
      icon: InstituteLogo,
    },
    {
      title: "Fraud Notifications",
      description: "Receive alerts for any tampered or forged documents.",
      icon: AlertLogo,
    },
    {
      title: "Secure Database",
      description: "Store and access your data securely in our database.",
      icon: ShieldLogo,
    },
  ];

  return (
    <div id="about" className="bg-white py-20 px-8 font-[Inter]">
      <div className="container mx-auto max-w-7xl">
        {/* About Section */}
        <div className="mb-16">
          <h2 className="text-4xl lg:text-5xl font-bold text-[#0A3258]">
            About
          </h2>
          <div className="flex flex-col lg:flex-row items-center lg:items-start lg:space-x-12 mt-8">
            {/* Image placeholder for About section */}
            <div className="w-full lg:w-1/2 flex justify-center mb-8 lg:mb-0">
              <img src={AboutLogo} alt="Logo" className="h-[270px] w-[310px]" />
            </div>
            <div className="w-full lg:w-1/2 text-center lg:text-left mt-2">
              <h3 className="text-4xl font-bold text-[#0A3258] mb-4">
                Our Mission: Ensuring Authenticity in Education
              </h3>
              <p className="text-lg text-gray-600">
                Authenex is committed to eliminating fraud in academic credentials. Our platform empowers institutions, employers, and individuals to instantly verify certificates with security, efficiency, and trust, fostering transparency and confidence in every educational milestone.
              </p>
            </div>
          </div>
        </div>

        {/* Features Section */}
        <div>
          <h2 className="text-4xl lg:text-5xl font-bold mb-8 text-[#0A3258] text-center">
            FEATURES
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <div key={index} className="bg-[#f0f4f9] p-18 rounded-lg text-center shadow-md">
                {/* Display individual feature icon */}
                <img
                  src={feature.icon}
                  alt={feature.title}
                  className="h-[50px] w-[50px] mx-auto mb-4"
                />
                <h3 className="text-2xl font-bold text-[#0A3258] mb-2">{feature.title}</h3>
                <p className="text-md text-gray-600">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default About;