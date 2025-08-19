export const mock = {
  blogs: [
    {
      id: "b1",
      title: "Shift-Left Security: Catch Issues Before Prod",
      excerpt:
        "Integrating security tests early reduces MTTR and prevents costly rollbacks. Learn the practical patterns.",
      tags: ["shift-left", "testing", "sast"],
      author: "Aisha Khan",
      date: "2025-07-21",
    },
    {
      id: "b2",
      title: "Policy as Code: Enforce Guardrails, Not Roadblocks",
      excerpt:
        "OPA/Rego and Kubernetes admission controls enable scalable security without slowing developers down.",
      tags: ["opa", "k8s", "policy"],
      author: "Liam Chen",
      date: "2025-06-12",
    },
    {
      id: "b3",
      title: "Secrets Management in CI/CD Done Right",
      excerpt:
        "From short-lived credentials to workload identity, see how modern pipelines eliminate secret sprawl.",
      tags: ["secrets", "identity", "cicd"],
      author: "Noah Patel",
      date: "2025-05-03",
    },
    {
      id: "b4",
      title: "Supply Chain Security: SBOMs, Signing, and Provenance",
      excerpt:
        "Sigstore, SLSA, and SBOMs form the backbone of resilient software supply chains.",
      tags: ["sbom", "slsa", "sigstore"],
      author: "Maya Rivera",
      date: "2025-08-02",
    },
    {
      id: "b5",
      title: "Runtime Security with eBPF: Observe, Detect, Respond",
      excerpt:
        "eBPF-based tooling delivers low-overhead, high-fidelity runtime visibility across clusters.",
      tags: ["ebpf", "runtime", "observability"],
      author: "Jon Park",
      date: "2025-04-14",
    },
    {
      id: "b6",
      title: "Threat Modeling for Cloud-Native Systems",
      excerpt:
        "Rapid, iterative threat modeling aligned with delivery cycles improves real risk coverage.",
      tags: ["threat-modeling", "cloud-native"],
      author: "Priya Singh",
      date: "2025-02-17",
    },
  ],
  tools: [
    {
      id: "t1",
      name: "Trivy",
      category: "Scanning",
      description: "Comprehensive scanner for containers, IaC, and code dependencies.",
      url: "https://aquasecurity.github.io/trivy/",
      tags: ["containers", "iac", "deps"],
    },
    {
      id: "t2",
      name: "Semgrep",
      category: "SAST",
      description: "Fast, developer-friendly static analysis with easy rules.",
      url: "https://semgrep.dev/",
      tags: ["sast", "code"],
    },
    {
      id: "t3",
      name: "Sigstore Cosign",
      category: "Supply Chain",
      description: "Sign, verify, and attest container images and artifacts.",
      url: "https://docs.sigstore.dev/cosign/overview/",
      tags: ["signing", "supply-chain"],
    },
    {
      id: "t4",
      name: "OPA / Rego",
      category: "Policy",
      description: "Policy-as-code engine to enforce guardrails in CI/CD and clusters.",
      url: "https://www.openpolicyagent.org/",
      tags: ["policy", "opa"],
    },
    {
      id: "t5",
      name: "Falco",
      category: "Runtime",
      description: "Runtime security detection engine powered by eBPF.",
      url: "https://falco.org/",
      tags: ["runtime", "ebpf"],
    },
    {
      id: "t6",
      name: "in-toto",
      category: "Supply Chain",
      description: "Framework to secure the integrity of software supply chains.",
      url: "https://in-toto.io/",
      tags: ["provenance", "supply-chain"],
    },
  ],
  path: [
    { id: "p1", label: "Foundations: Git, Linux, Networking", durationMin: 240 },
    { id: "p2", label: "Containers: Docker Essentials", durationMin: 180 },
    { id: "p3", label: "Kubernetes: Core Workloads", durationMin: 300 },
    { id: "p4", label: "CI/CD: Pipelines & GitOps", durationMin: 240 },
    { id: "p5", label: "Security: SAST, DAST, IaC Scanning", durationMin: 240 },
    { id: "p6", label: "Supply Chain: SBOMs & Signing", durationMin: 180 },
    { id: "p7", label: "Runtime: Observability & eBPF", durationMin: 180 },
  ],
  channels: [
    { id: "c1", name: "#general" },
    { id: "c2", name: "#devsecops-news" },
    { id: "c3", name: "#help" },
  ],
  initialMessages: {
    "#general": [
      { id: "m1", author: "System", text: "Welcome to the DevSecOps community!", ts: Date.now() - 86400000 },
    ],
    "#devsecops-news": [
      { id: "m2", author: "Bot", text: "New post: Sigstore and SLSA in action.", ts: Date.now() - 3600000 },
    ],
    "#help": [
      { id: "m3", author: "System", text: "Ask questions and help others.", ts: Date.now() - 7200000 },
    ],
  },
};