CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    bio TEXT, avatar_url VARCHAR(500), github_username VARCHAR(100),
    website VARCHAR(255), country VARCHAR(100),
    rating INT NOT NULL DEFAULT 1000, max_rating INT NOT NULL DEFAULT 1000,
    rating_volatility FLOAT NOT NULL DEFAULT 250.0,
    total_solved INT NOT NULL DEFAULT 0, total_points INT NOT NULL DEFAULT 0,
    total_competitions INT NOT NULL DEFAULT 0, competition_wins INT NOT NULL DEFAULT 0,
    consecutive_days INT NOT NULL DEFAULT 0, last_active_date DATE,
    role VARCHAR(50) NOT NULL DEFAULT 'user',
    is_verified BOOLEAN NOT NULL DEFAULT FALSE,
    is_banned BOOLEAN NOT NULL DEFAULT FALSE, ban_reason TEXT,
    last_login TIMESTAMP WITH TIME ZONE,
    deleted_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS challenges (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(200) NOT NULL, slug VARCHAR(200) UNIQUE NOT NULL,
    description TEXT NOT NULL, category VARCHAR(50) NOT NULL,
    difficulty VARCHAR(50) NOT NULL,
    base_points INT NOT NULL DEFAULT 100,
    min_points INT DEFAULT 50, max_points INT DEFAULT 500,
    decay_rate FLOAT DEFAULT 0.95, current_points INT DEFAULT 100,
    flag_hash VARCHAR(255) NOT NULL, flag_format VARCHAR(50) DEFAULT 'CTF{...}',
    hints JSONB DEFAULT '[]', files JSONB DEFAULT '[]', tags TEXT[] DEFAULT '{}',
    prerequisites UUID[] DEFAULT '{}',
    author_id UUID NOT NULL REFERENCES users(id),
    total_attempts INT NOT NULL DEFAULT 0, total_solves INT NOT NULL DEFAULT 0,
    total_likes INT NOT NULL DEFAULT 0,
    first_blood_user_id UUID REFERENCES users(id),
    first_blood_at TIMESTAMP WITH TIME ZONE,
    is_dynamic_scoring BOOLEAN NOT NULL DEFAULT TRUE,
    is_hidden BOOLEAN NOT NULL DEFAULT FALSE,
    is_draft BOOLEAN NOT NULL DEFAULT FALSE,
    allow_writeups BOOLEAN NOT NULL DEFAULT TRUE,
    published_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS submissions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id),
    challenge_id UUID NOT NULL REFERENCES challenges(id),
    submitted_flag TEXT NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    points_earned INT NOT NULL DEFAULT 0,
    attempt_number INT NOT NULL DEFAULT 1,
    ip_address INET, user_agent TEXT,
    submitted_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS rating_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id),
    rating_before INT NOT NULL, rating_after INT NOT NULL,
    rating_change INT NOT NULL,
    contest_id UUID, challenge_id UUID REFERENCES challenges(id),
    reason VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS announcements (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(200) NOT NULL, content TEXT NOT NULL,
    is_pinned BOOLEAN DEFAULT FALSE,
    created_by UUID NOT NULL REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS teams (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) UNIQUE NOT NULL, description TEXT,
    avatar_url VARCHAR(500),
    captain_id UUID NOT NULL REFERENCES users(id),
    team_code VARCHAR(20) UNIQUE NOT NULL,
    status VARCHAR(50) DEFAULT 'active',
    total_members INT DEFAULT 1, team_rating INT DEFAULT 1000,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS team_members (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    team_id UUID NOT NULL REFERENCES teams(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id),
    role VARCHAR(50) DEFAULT 'member',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS achievements (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL, description TEXT,
    type VARCHAR(50) NOT NULL, required_value INT DEFAULT 1,
    points_reward INT DEFAULT 0, icon_url VARCHAR(500),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS user_achievements (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id),
    achievement_id UUID NOT NULL REFERENCES achievements(id),
    progress INT DEFAULT 0, is_completed BOOLEAN DEFAULT FALSE,
    completed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS writeups (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id),
    challenge_id UUID NOT NULL REFERENCES challenges(id),
    title VARCHAR(200) NOT NULL, content TEXT NOT NULL,
    is_published BOOLEAN DEFAULT FALSE,
    total_likes INT DEFAULT 0, total_views INT DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_users_rating ON users(rating DESC);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_challenges_category ON challenges(category);
CREATE INDEX IF NOT EXISTS idx_challenges_difficulty ON challenges(difficulty);
CREATE INDEX IF NOT EXISTS idx_submissions_user ON submissions(user_id);
CREATE INDEX IF NOT EXISTS idx_submissions_challenge ON submissions(challenge_id);
CREATE INDEX IF NOT EXISTS idx_submissions_status ON submissions(status);

INSERT INTO users (username, email, password_hash, full_name, role, is_verified) 
VALUES ('admin', 'admin@cybersec.az', crypt('Admin123!@#', gen_salt('bf')), 'System Admin', 'super_admin', TRUE)
ON CONFLICT (username) DO NOTHING;

INSERT INTO users (username, email, password_hash, full_name, role, is_verified) 
VALUES ('moderator', 'mod@cybersec.az', crypt('Mod123!@#', gen_salt('bf')), 'Club Moderator', 'moderator', TRUE)
ON CONFLICT (username) DO NOTHING;

INSERT INTO challenges (title, slug, description, category, difficulty, base_points, flag_hash, author_id)
VALUES ('SQL Injection Basics', 'sql-injection-basics', 'Find the SQL injection vulnerability in the login form and gain admin access.', 'web_exploitation', 'easy', 100, crypt('CTF{sql_injection_master}', gen_salt('bf')), (SELECT id FROM users WHERE username = 'admin'))
ON CONFLICT (slug) DO NOTHING;

INSERT INTO challenges (title, slug, description, category, difficulty, base_points, flag_hash, author_id)
VALUES ('RSA Weak Key', 'rsa-weak-key', 'Decrypt the message encrypted with a weak RSA key. Factor the modulus to find the private key.', 'cryptography', 'medium', 200, crypt('CTF{rsa_crack_success}', gen_salt('bf')), (SELECT id FROM users WHERE username = 'admin'))
ON CONFLICT (slug) DO NOTHING;

INSERT INTO challenges (title, slug, description, category, difficulty, base_points, flag_hash, author_id)
VALUES ('Memory Dump Analysis', 'memory-dump', 'Analyze the provided memory dump file to extract hidden credentials and find the flag.', 'forensics', 'hard', 300, crypt('CTF{memory_analysis_pro}', gen_salt('bf')), (SELECT id FROM users WHERE username = 'admin'))
ON CONFLICT (slug) DO NOTHING;
