import React, { useState } from 'react'

const App = () => {

  const [a, setA] = useState(10)

  const changeNumb = () =>{
    setA (20)
  }



  // let namee = 'Aman'

  // const changenam = 'Rahul'

  // const changeName = () =>[
  //   console.log(namee),
  //    namee = "rohit",
  //   console.log(namee)
  // ]

  // const age =21

  // const abc = () =>{
  //   console.log("Hello")
  // }

  return (
    <div>
      {/* <h1>Hi my name is Aman and my age is {age}</h1>
      <button onClick={abc}>click me</button> */}

      {/* <h1>my name is {namee}</h1>
      <button onClick={changeName}>click me to change name</button>  */}

      {/* soo see onclick karke name change nahi hoga. console mai to change ho raha hhai but frontend mai  nahi dikh raha. you know uske lia hame react ke hisab se chanlna hoga. hamne ese const a=10 ab ese variables banna chodna padega. ab hamme hooks ka use karna hoga. like usestae */}



      <h1 className='text-5xl'>The value of a is : {a}</h1>
      <button onClick={changeNumb}>click me to chgane the value</button>
    </div>
  )
}

export default App