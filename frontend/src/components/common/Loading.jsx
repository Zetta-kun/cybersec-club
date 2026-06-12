import React from 'react';
const Loading = ({ message = 'Yüklənir...' }) => (<div className='flex flex-col items-center justify-center py-20'><div className='w-12 h-12 border-4 border-cyber-500 border-t-transparent rounded-full animate-spin mb-4'></div><p className='text-gray-400'>{message}</p></div>);
export default Loading;
