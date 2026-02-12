import { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { FaPaperPlane, FaFileUpload, FaYoutube, FaFilePdf, FaFileWord, FaImage, FaRobot, FaUser } from 'react-icons/fa';
import './App.css';

function App() {
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState([
    { role: 'ai', content: 'Hello! Upload a document or video link, and I can answer questions about it.' }
  ]);
  const [file, setFile] = useState(null);
  const [url, setUrl] = useState('');
  const [type, setType] = useState('pdf');
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  
  const chatEndRef = useRef(null);

  // Auto-scroll to bottom of chat
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleUpload = async () => {
    if (!file && !url) return alert("Please select a file or enter a URL");
    
    setUploading(true);
    const formData = new FormData();
    formData.append('type', type);
    if (url) formData.append('url', url);
    if (file) formData.append('file', file);

    try {
      const res = await axios.post('http://localhost:8000/upload', formData);
      alert(`Success: ${res.data.message}`);
      setFile(null);
      setUrl('');
    } catch (err) {
      alert("Error uploading file. Check backend console.");
    }
    setUploading(false);
  };

  const handleChat = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    const newMsgs = [...messages, { role: 'user', content: query }];
    setMessages(newMsgs);
    setQuery('');
    setLoading(true);

    const formData = new FormData();
    formData.append('query', query);

    try {
      const res = await axios.post('http://localhost:8000/chat', formData);
      setMessages([...newMsgs, { role: 'ai', content: res.data.answer }]);
    } catch (err) {
      setMessages([...newMsgs, { role: 'ai', content: "Sorry, I encountered an error connecting to the server." }]);
    }
    setLoading(false);
  };

  return (
    <div className="app-container">
      {/* Sidebar - Knowledge Base */}
      <div className="sidebar">
        <h2><FaRobot /> Knowledge Base</h2>
        <p className="subtitle">Feed your AI context here.</p>
        
        <div className="upload-section">
          <label>Source Type</label>
          <div className="type-selector">
            <button className={type === 'pdf' ? 'active' : ''} onClick={() => setType('pdf')}><FaFilePdf /> PDF</button>
            <button className={type === 'doc' ? 'active' : ''} onClick={() => setType('doc')}><FaFileWord /> Doc</button>
            <button className={type === 'image' ? 'active' : ''} onClick={() => setType('image')}><FaImage /> OCR</button>
            <button className={type === 'video' ? 'active' : ''} onClick={() => setType('video')}><FaYoutube /> Video</button>
          </div>

          {type === 'video' ? (
            <input 
              type="text" 
              className="input-field" 
              placeholder="Paste YouTube Link..." 
              value={url}
              onChange={(e) => setUrl(e.target.value)} 
            />
          ) : (
            <div className="file-input-wrapper">
              <input type="file" id="file-upload" onChange={(e) => setFile(e.target.files[0])} />
              <label htmlFor="file-upload" className="file-label">
                {file ? file.name : "Choose File..."} <FaFileUpload />
              </label>
            </div>
          )}

          <button onClick={handleUpload} disabled={uploading} className="upload-btn">
            {uploading ? 'Processing...' : 'Upload & Process'}
          </button>
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="chat-area">
        <div className="chat-header">
          <h3>Multimodal RAG Assistant</h3>
        </div>

        <div className="messages-container">
          {messages.map((m, i) => (
            <div key={i} className={`message ${m.role}`}>
              <div className="avatar">
                {m.role === 'ai' ? <FaRobot /> : <FaUser />}
              </div>
              <div className="bubble">
                {m.content}
              </div>
            </div>
          ))}
          {loading && <div className="message ai"><div className="bubble">Thinking...</div></div>}
          <div ref={chatEndRef} />
        </div>

        <form className="input-area" onSubmit={handleChat}>
          <input 
            value={query} 
            onChange={(e) => setQuery(e.target.value)} 
            placeholder="Ask something about your documents..." 
          />
          <button type="submit" disabled={loading}>
            <FaPaperPlane />
          </button>
        </form>
      </div>
    </div>
  );
}

export default App;