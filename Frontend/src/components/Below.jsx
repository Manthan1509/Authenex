import React from 'react';
import BelowLogo1 from '../assets/Below_image_1-remove.png';
import BelowLogo2 from '../assets/Below_image_2-remove.png';
import BelowLogo3 from '../assets/Below_image_3-remove.png';

const Below = () => {
  const steps = [
    {
      number: 1, // Still keep the number for key, but won't display
      title: "UPLOAD CERTIFICATES IN BULK",
      description: "Easily upload certificates from your organization, institute, or applicants for verification.",
      icon: BelowLogo1
    },
    {
      number: 2, // Still keep the number for key, but won't display
      title: "REQUEST VERIFICATION INSTANTLY.",
      description: "Submit verification requests securely and track them in real-time.",
      icon: BelowLogo2
    },
    {
      number: 3, // Still keep the number for key, but won't display
      title: "RECEIVE YOUR E-VERIFIED CERTIFICATE",
      description: "Get authenticated certificates delivered digitally, ensuring trust and compliance.",
      icon: BelowLogo3
    },
  ];

  return (
    <div className="bg-[#edf7ff] py-20 px-8 font-[Inter]">
      <div className="container mx-auto max-w-7xl">
        <h2 className="text-4xl lg:text-5xl font-bold text-center mb-16 text-[#0A3258]">
          HOW IT WORKS
        </h2>
        <div className="flex flex-col lg:flex-row items-center justify-center space-y-12 lg:space-y-0 lg:space-x-12 lg:px-3">
          {steps.map((step) => (
            <div key={step.number} className="flex flex-col items-center text-center">
              <div className="relative w-65 h-65 flex items-center justify-center mb-4"> {/* Increased size to w-60 h-60 and added mb-4 */}
                <img 
                  src={step.icon} 
                  alt={`Step ${step.number} icon`} 
                  className="w-full h-full object-contain"
                />
              </div>
              {/* Removed the div that displayed the step number */}
              <h3 className="mt-3 text-xl font-bold text-[#0A3258] uppercase tracking-wide">
                {step.title}
              </h3>
              <p className="mt-3 lg:mt-4 text-lg font-medium text-gray-600 max-w-xs">
                {step.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Below;
