
import React, { useState } from 'react';
import axios from 'axios';

const ChatInterface = () => {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([
    { role: 'system', content: '你是一个聪明且富有创造力的小说作家' },
    { role: 'user', content: '请你作为童话故事大王，写一篇短篇童话故事，故事的主题是要永远保持一颗善良的心，要能够激发儿童的学习兴趣和想象力，同时也能够帮助儿童更好地理解和接受故事中所蕴含的道理和价值观。' },
  ]);

  const handleInputChange = (e) => {
    setInput(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const newMessage = { role: 'user', content: input };
    setMessages([...messages, newMessage]);
    const response = await axios.post('https://open.bigmodel.cn/api/paas/v4/chat/completions/create', {
      model: 'glm-4-flash',
      messages: [...messages, newMessage],
      stream: true,
    });
    const chunks = response.data;
    for (const chunk of chunks) {
      console.log(chunk.choices[0].delta.content, end="");
    }
    setInput('');
  };

  return (
    <Container maxWidth="sm">
      <Box sx={{ display: 'flex', flexDirection: 'column', height: '500px', border: '1px solid #ddd', borderRadius: '5px', padding: '10px', marginTop: '20px' }}>
        {messages.map((message, index) => (
          <Box key={index} sx={{ marginBottom: '10px', padding: '10px', borderRadius: '5px', backgroundColor: message.role === 'system' ? '#f5f5f5' : '#e0e0e0', alignSelf: message.role === 'system' ? 'flex-start' : 'flex-end' }}>
            <Typography variant="body1">{message.content}</Typography>
          </Box>
        ))}
      </Box>
      <form onSubmit={handleSubmit}>
        <TextField
          fullWidth
          variant="outlined"
          value={input}
          onChange={handleInputChange}
          placeholder="Type your message here..."
          sx={{ marginBottom: '10px' }}
        />
        <Button type="submit" variant="contained" color="primary" sx={{ marginBottom: '10px' }}>
          Submit
        </Button>
      </form>
    </Container>
  );
};

export default ChatInterface;
