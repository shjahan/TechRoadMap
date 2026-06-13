# 📚 فهرست فایل‌های آموزشی Senior Java / Tech Lead

> این فایل‌ها از روی `senior_java_roadmap` تولید شده‌اند. هر فایل برای یک section است و شامل: مفاهیم عمیق با کد واقعی، سوالات مصاحبه‌ی Senior/Lead با جواب کامل، اشتباهات رایج (کد قبل/بعد)، و ارتباط با سایر مفاهیم.

---

## 1. Java — از ابتدا تا Java 25

- [مبانی زبان Java (Java 1–8)](1_1_java_language_fundamentals.md) — OOP, SOLID, Collections, Generics, Memory
- [Java 8 — نقطه عطف](1_2_java_8_turning_point.md) — Lambda, Stream, Optional, java.time
- [Java 9–11](1_3_java_9_11.md) — Modules, var, HTTP Client
- [Java 12–17 (LTS)](1_4_java_12_17_lts.md) — Records, Sealed, Pattern Matching
- [Java 18–21](1_5_java_18_21.md) — Virtual Threads, Record Patterns
- [Java 22–25 + Concurrency + JVM](1_6_java_22_25_concurrency_jvm.md) — Gatherers, Scoped Values, JMM

## 2. Spring Ecosystem

- [Spring Core](2_1_spring_core.md) — IoC, DI, AOP, Events
- [Spring Boot](2_2_spring_boot.md) — Auto-Config, Actuator, Boot 4
- [Spring MVC & WebFlux](2_3_spring_mvc_webflux.md) — REST, Reactive, HTTP Clients
- [Spring Data](2_4_spring_data.md) — JPA, Transactions, N+1, Locking
- [Spring Security](2_5_spring_security.md) — Auth, OAuth2, Keycloak
- [Spring Cloud](2_6_spring_cloud.md) — Discovery, Gateway, Resilience, Tracing

## 3. Relational Databases

- [مبانی SQL](3_1_sql_fundamentals.md) — DDL, DML, Joins, Window Functions
- [Indexing & Performance](3_2_indexing_performance.md) — Index Types, EXPLAIN, Pooling
- [PostgreSQL](3_3_postgresql.md) — JSONB, MVCC, Replication
- [MySQL / Oracle](3_4_mysql_oracle.md) — مقایسه‌ای

## 4. MongoDB

- [مبانی MongoDB](4_1_mongodb_basics.md) — مدل داده, CRUD
- [Aggregation Pipeline](4_2_aggregation_pipeline.md)
- [Indexing](4_3_mongodb_indexing.md)
- [Transactions & Replication](4_4_transactions_replication.md) — Sharding
- [Performance & Spring Data MongoDB](4_5_performance_spring_data_mongodb.md)

## 5. Data Structures & Algorithms

- [Data Structures](5_1_data_structures.md) — HashMap internals, Tree, Graph
- [Algorithms](5_2_algorithms.md) — Sorting, DP, Greedy, Complexity
- [Design Patterns (GoF)](5_3_design_patterns.md)

## 6. Architecture & System Design

- [Architectural Patterns](6_1_architectural_patterns.md) — Microservices, DDD, CQRS, SAGA
- [System Design](6_2_system_design.md) — CAP, Caching, Rate Limiting

## 7. Security

- [مبانی امنیت](7_1_security_fundamentals.md) — OWASP, Injection, XSS, CSRF
- [OAuth 2.0, OIDC, JWT, Keycloak](7_2_oauth_oidc_keycloak.md)

## 8. Message Brokers

- [Apache Kafka](8_1_apache_kafka.md) — Delivery, Streams
- [RabbitMQ](8_2_rabbitmq.md) — Exchanges, Reliability
- [MQTT](8_3_mqtt.md) — IoT, QoS

## 9. Caching

- [Redis](9_1_redis.md) — Data Types, Lock, Spring Cache
- [Hazelcast](9_2_hazelcast.md) — In-Memory Data Grid

## 10. DevOps

- [Docker](10_1_docker.md)
- [Kubernetes](10_2_kubernetes.md) — Probes, Scaling, Resources
- [CI/CD](10_3_cicd.md)
- [Monitoring & Observability](10_4_monitoring_observability.md)
- [Infrastructure as Code](10_5_infrastructure_as_code.md)

## 11. Frontend

- [React 19](11_1_react_19.md)
- [Next.js 16](11_2_nextjs_16.md)

## 12. Java — تکمیلی و عمیق‌تر

- [Java Memory Model](12_1_java_memory_model.md)
- [Reflection & Dynamic Proxy](12_2_reflection_dynamic_proxy.md)
- [Java I/O & NIO](12_3_java_io_nio.md)
- [Serialization](12_4_serialization.md)
- [Testing](12_5_testing.md) — JUnit, Mockito, Testcontainers
- [JVM Internals عمیق](12_6_jvm_internals_deep.md) — GC, JIT, JFR

## 13. Spring — تکمیلی

- [Spring Batch](13_1_spring_batch.md)
- [Spring Integration](13_2_spring_integration.md)
- [Spring Authorization Server](13_3_spring_authorization_server.md)
- [Reactive Programming عمیق](13_4_reactive_programming.md)
- [Spring Boot Testing عمیق](13_5_spring_boot_testing_deep.md)

## 14. Database — تکمیلی

- [Query Optimization عمیق](14_1_query_optimization_deep.md)
- [Advanced PostgreSQL](14_2_advanced_postgresql.md) — RLS, JSONB, FTS
- [Database Design Patterns](14_3_database_design_patterns.md)

## 15. Architecture — تکمیلی

- [Clean / Hexagonal Architecture](15_1_clean_hexagonal_architecture.md)
- [Resilience Patterns عمیق](15_2_resilience_patterns_deep.md)
- [12-Factor App](15_3_twelve_factor_app.md)
- [gRPC](15_4_grpc.md)

## 16. DevOps — تکمیلی

- [Helm](16_1_helm.md)
- [Terraform](16_2_terraform.md)
- [GitOps با ArgoCD](16_3_gitops_argocd.md)
- [Observability عمیق](16_4_observability_deep.md)
- [DevSecOps](16_5_devsecops.md)

## 17. Elasticsearch

- [مفاهیم پایه](17_1_elasticsearch_basics.md)
- [CRUD و Search](17_2_crud_and_search.md)
- [Spring Data Elasticsearch](17_3_spring_data_elasticsearch.md)
- [Index Management](17_4_index_management.md)

## 18. Frontend — تکمیلی

- [TypeScript](18_1_typescript.md)
- [State Management عمیق](18_2_state_management_deep.md)
- [Performance Patterns](18_3_performance_patterns.md)

## 19. مفاهیم مکمل

- [API Design عمیق](19_1_api_design_deep.md)
- [Idempotency](19_2_idempotency.md)
- [Distributed Tracing عملی](19_3_distributed_tracing.md)
- [Event Storming](19_4_event_storming.md)
- [Interview Preparation](19_5_interview_preparation.md)

---

**مجموع: ۷۵ فایل آموزشی** پوشش‌دهنده‌ی تمام sectionهای roadmap.
