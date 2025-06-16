# OBDA实证分析：大学数据库本体推理演示

## 实验目的

通过一个简单的大学数据库案例，演示：
1. OBDA如何将关系数据库映射到语义层
2. 本体推理如何丰富查询结果
3. SPARQL查询相比SQL的优势

## 快速开始

1. 启动SPARQL端点：
   ```bash
   ./start_endpoint.sh
   ```

2. 运行示例查询：
   ```bash
   ./run_all_queries.sh
   ```

3. 对比SQL查询：
   ```bash
   ./verify_sql.sh
   ```

## 关键概念演示

### 1. 子类推理
- 查询`Person`自动包含所有`Employee`和`Student`
- 查询`AcademicStaff`自动包含`Professor`、`AssociateProfessor`和`Lecturer`

### 2. 等价类推理
- `Teacher`被定义为"有教学任务的员工"
- 系统自动推理出谁是Teacher

### 3. 多层推理
- `Professor`是`AcademicStaff`的子类
- `AcademicStaff`是`Employee`的子类
- `Employee`是`Person`的子类
- 查询`Person`时，`Professor`会被包含

## 查询说明

1. **01_all_persons.sparql**: 展示Person类的推理
2. **02_academic_staff.sparql**: 展示多层子类推理
3. **03_teachers.sparql**: 展示等价类推理
4. **04_supervisors.sparql**: 展示反向属性推理
5. **05_graduate_info.sparql**: 展示复杂查询
6. **06_dept_teaching_load.sparql**: 展示聚合查询

## 推理效果对比

| 查询目标 | SQL结果 | SPARQL+推理结果 | 差异原因 |
|---------|---------|----------------|---------|
| 所有Person | 无法查询 | 9条 | SQL无Person概念，SPARQL推理包含所有子类 |
| 所有Teacher | 需要复杂JOIN | 3条 | SPARQL自动推理等价类定义 |
| 所有AcademicStaff | 需要OR条件 | 4条 | SPARQL自动包含所有子类 |

## 技术架构

```
用户 <--SPARQL--> Ontop <--SQL--> MySQL
                    |
                 本体+映射
                    |
                  推理引擎
```

## 深入学习

1. 修改本体文件，添加新的类或属性
2. 修改映射文件，尝试不同的映射策略
3. 编写新的SPARQL查询，探索推理能力
4. 使用调试模式查看查询重写过程：
   ```bash
   ./run_query.sh queries/01_all_persons.sparql --log-level=DEBUG
   ```
