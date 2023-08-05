from localstack.utils.aws import aws_models
vRusL=super
vRusl=None
vRusI=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  vRusL(LambdaLayer,self).__init__(arn)
  self.cwd=vRusl
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.vRusI.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,vRusI,env=vRusl):
  vRusL(RDSDatabase,self).__init__(vRusI,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,vRusI,env=vRusl):
  vRusL(RDSCluster,self).__init__(vRusI,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,vRusI,env=vRusl):
  vRusL(AppSyncAPI,self).__init__(vRusI,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,vRusI,env=vRusl):
  vRusL(AmplifyApp,self).__init__(vRusI,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,vRusI,env=vRusl):
  vRusL(ElastiCacheCluster,self).__init__(vRusI,env=env)
class TransferServer(BaseComponent):
 def __init__(self,vRusI,env=vRusl):
  vRusL(TransferServer,self).__init__(vRusI,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,vRusI,env=vRusl):
  vRusL(CloudFrontDistribution,self).__init__(vRusI,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,vRusI,env=vRusl):
  vRusL(CodeCommitRepository,self).__init__(vRusI,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
