import React, { ReactNode } from 'react';
import { Avatar, Tooltip } from 'antd';
import './style.css';

interface CommentProps {
  author: string;
  avatar: ReactNode;
  content: ReactNode;
  datetime: ReactNode;
  actions?: ReactNode[];
}

const Comment: React.FC<CommentProps> = ({ 
  author, 
  avatar, 
  content, 
  datetime, 
  actions 
}) => {
  return (
    <div className="ant-comment">
      <div className="ant-comment-inner">
        <div className="ant-comment-avatar">
          {avatar}
        </div>
        <div className="ant-comment-content">
          <div className="ant-comment-content-author">
            <span className="ant-comment-content-author-name">{author}</span>
            <span className="ant-comment-content-author-time">{datetime}</span>
          </div>
          <div className="ant-comment-content-detail">{content}</div>
          {actions && actions.length > 0 && (
            <ul className="ant-comment-actions">
              {actions.map((action, index) => (
                <li key={`action-${index}`}>{action}</li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
};

export default Comment;