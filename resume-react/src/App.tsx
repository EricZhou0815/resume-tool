import { useState, useEffect } from 'react'

interface ResumeData {
  name: string
  title: string
  email: string
  phone: string
  linkedin?: string
  github?: string
  summary: string
  experiences: Experience[]
  skill_groups: SkillGroup[]
  projects: Project[]
  education: Education[]
  languages: Language[]
}

interface Experience {
  company: string
  position: string
  period: string
  location?: string
  highlights: string[]
}

interface SkillGroup {
  category: string
  skill_list: string[]
}

interface Project {
  name: string
  description: string
  tech: string
  highlights: string[]
}

interface Education {
  institution: string
  degree: string
  field?: string
  start_date?: string
  end_date?: string
  grade?: string
}

interface Language {
  language: string
  level: string
}

const TEMPLATES = ['modern', 'classic', 'investment-bank', 'sidebar']

function App() {
  const [data, setData] = useState<ResumeData | null>(null)
  const [template, setTemplate] = useState('modern')

  useEffect(() => {
    fetch('/resume-data.json')
      .then(r => r.json())
      .then(setData)
      .catch(() => console.error('Failed to load resume data'))
  }, [])

  if (!data) return <div style={{padding:40,textAlign:'center',color:'#999'}}>Loading...</div>

  return (
    <div>
      <div className="switcher-bar">
        <label htmlFor="tpl-select">Template:</label>
        <select id="tpl-select" value={template} onChange={e => setTemplate(e.target.value)}>
          {TEMPLATES.map(t => (
            <option key={t} value={t}>{t.replace('-', ' ').replace(/\b\w/g, c => c.toUpperCase())}</option>
          ))}
        </select>
      </div>
      <div className="page-wrap">
        {template === 'modern' && <ModernTemplate data={data} />}
        {template === 'classic' && <ClassicTemplate data={data} />}
        {template === 'investment-bank' && <IBTemplate data={data} />}
        {template === 'sidebar' && <SidebarTemplate data={data} />}
      </div>
    </div>
  )
}

function ModernTemplate({ data }: { data: ResumeData }) {
  return (
    <div className="page modern-page">
      <div className="modern-header">
        <h1>{data.name}</h1>
        <div className="modern-title">{data.title}</div>
        <div className="modern-contact">
          <span>Email: {data.email}</span>
          <span>Phone: {data.phone}</span>
          {data.linkedin && <span>LinkedIn: {data.linkedin}</span>}
          {data.github && <span>GitHub: {data.github}</span>}
        </div>
      </div>
      <div className="modern-body">
        {data.summary && (
          <div className="section">
            <h2>Summary</h2>
            <p>{data.summary}</p>
          </div>
        )}
        {data.experiences.map((exp, i) => (
          <div key={i} className="entry">
            <div className="entry-header">
              <h3>{exp.position} · {exp.company}</h3>
              <span className="period">{exp.period}</span>
            </div>
            {exp.location && <div className="subtitle">{exp.location}</div>}
            <ul>{exp.highlights.map((h, j) => <li key={j}>{h}</li>)}</ul>
          </div>
        ))}
        <div className="section">
          <h2>Skills</h2>
          <div className="skills-grid">
            {data.skill_groups.map((g, i) => (
              <div key={i}>
                <h4>{g.category}</h4>
                <div className="skill-tags">{g.skill_list.map((s, j) => <span key={j}>{s}</span>)}</div>
              </div>
            ))}
          </div>
        </div>
        {data.projects.length > 0 && (
          <div className="section">
            <h2>Projects</h2>
            {data.projects.map((p, i) => (
              <div key={i} className="entry">
                <h3>{p.name}</h3>
                <p style={{color:'#64748b',fontSize:14}}>{p.description}</p>
                <div className="project-tech">{p.tech}</div>
                <ul>{p.highlights.map((h, j) => <li key={j}>{h}</li>)}</ul>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

function ClassicTemplate({ data }: { data: ResumeData }) {
  return (
    <div className="page classic-page">
      <div className="classic-header">
        <h1>{data.name}</h1>
        <div className="classic-title">{data.title}</div>
        <div className="classic-contact">
          <span>Email: {data.email}</span>
          <span>Phone: {data.phone}</span>
          {data.linkedin && <span>LinkedIn: {data.linkedin}</span>}
          {data.github && <span>GitHub: {data.github}</span>}
        </div>
      </div>
      {data.summary && (
        <div className="classic-section">
          <h2>Summary</h2>
          <p>{data.summary}</p>
        </div>
      )}
      <div className="classic-section">
        <h2>Experience</h2>
        {data.experiences.map((exp, i) => (
          <div key={i} className="classic-entry">
            <div className="classic-entry-header">
              <strong>{exp.position}, {exp.company}</strong>
              <span className="period">{exp.period}</span>
            </div>
            <ul>{exp.highlights.map((h, j) => <li key={j}>{h}</li>)}</ul>
          </div>
        ))}
      </div>
      <div className="classic-section">
        <h2>Skills</h2>
        {data.skill_groups.map((g, i) => (
          <div key={i}><strong>{g.category}:</strong> {g.skill_list.join(', ')}</div>
        ))}
      </div>
    </div>
  )
}

function IBTemplate({ data }: { data: ResumeData }) {
  return (
    <div className="page ib-page">
      <div className="ib-header">
        <div>
          <h1>{data.name}</h1>
          <div className="ib-title">{data.title}</div>
        </div>
        <div className="ib-contact">
          <div>{data.phone}</div>
          <div>{data.email}</div>
          {data.linkedin && <div>LinkedIn: {data.linkedin}</div>}
          {data.github && <div>GitHub: {data.github}</div>}
        </div>
      </div>
      {data.summary && (
        <div className="ib-section">
          <h2>Professional Summary</h2>
          <p>{data.summary}</p>
        </div>
      )}
      <div className="ib-section">
        <h2>Experience</h2>
        {data.experiences.map((exp, i) => (
          <div key={i} className="ib-entry">
            <div className="ib-entry-header">
              <strong>{exp.position}</strong>
              <span>{exp.period}</span>
            </div>
            <div className="ib-company">{exp.company}</div>
            <ul>{exp.highlights.map((h, j) => <li key={j}>{h}</li>)}</ul>
          </div>
        ))}
      </div>
      <div className="ib-section">
        <h2>Skills & Expertise</h2>
        <div className="ib-skills">
          {data.skill_groups.map((g, i) => (
            <div key={i}><strong>{g.category}:</strong> {g.skill_list.join(', ')}</div>
          ))}
        </div>
      </div>
    </div>
  )
}

function SidebarTemplate({ data }: { data: ResumeData }) {
  const sideSkillGroups = data.skill_groups.filter((_, i) => i % 2 === 0)
  const mainSkillGroups = data.skill_groups.filter((_, i) => i % 2 !== 0)

  return (
    <div className="page sb-page">
      <div className="sb-sidebar">
        <div className="sb-name">{data.name}</div>
        <div className="sb-title">{data.title}</div>

        <div className="sb-section">
          <h2>Contact</h2>
          <div className="sb-contact">{data.email}</div>
          <div className="sb-contact">{data.phone}</div>
          {data.linkedin && <div className="sb-contact">{data.linkedin}</div>}
          {data.github && <div className="sb-contact">{data.github}</div>}
        </div>

        <div className="sb-section">
          <h2>Skills</h2>
          {data.skill_groups.map((g, i) => (
            <div key={i} style={{marginBottom:8}}>
              <div className="sb-skill-cat">{g.category}</div>
              {g.skill_list.map((s, j) => (
                <span key={j} className="sb-skill-tag">{s}</span>
              ))}
            </div>
          ))}
        </div>

        {data.languages.length > 0 && (
          <div className="sb-section">
            <h2>Languages</h2>
            {data.languages.map((l, i) => (
              <div key={i} className="sb-contact">{l.language} — {l.level}</div>
            ))}
          </div>
        )}
      </div>
      <div className="sb-main">
        {data.summary && (
          <div className="sb-main-section">
            <h2>Summary</h2>
            <p>{data.summary}</p>
          </div>
        )}
        <div className="sb-main-section">
          <h2>Experience</h2>
          {data.experiences.map((exp, i) => (
            <div key={i} style={{marginBottom:16}}>
              <div className="sb-exp-header">
                <strong>{exp.position}, {exp.company}</strong>
                <span className="sb-period">{exp.period}</span>
              </div>
              <ul style={{fontSize:'13px',lineHeight:1.5, marginLeft:16}}>
                {exp.highlights.map((h, j) => <li key={j}>{h}</li>)}
              </ul>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default App
