import React from 'react';
const ErrorMessage = ({ message = 'Xəta baş verdi', onRetry }) => (<div className='flex flex-col items-center justify-center py-20 text-center'><div className='text-5xl mb-4'>⚠️</div><h2 className='text-xl font-semibold text-red-400 mb-2'>Xəta!</h2><p className='text-gray-400 mb-4'>{message}</p>{onRetry && <button onClick={onRetry} className='cyber-btn-primary'>Yenidən cəhd et</button>}</div>);
export default ErrorMessage;
